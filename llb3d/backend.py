import tempfile
import pathlib
import shutil
import glob
import subprocess
import sys
import os
import ctypes
import multiprocessing

from llvmlite import ir, binding

SOURCE_DIRECTORY = pathlib.Path(__file__).parent.resolve() / 'bbprogram'
SOURCE_FILENAME = 'bbprogram.s'
EXECUTABLE_FILENAME = 'bbprogram'
SYSTEM_SHARED = pathlib.Path('/usr/lib/x86_64-linux-gnu')

# All these initializations are required for code generation!
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()  # yes, even this one

# Load libraries
def load_shared_library(name):
    """Find and load shared library."""
    if (SOURCE_DIRECTORY / name).exists():
        binding.load_library_permanently(str(SOURCE_DIRECTORY / name))
    else:
        binding.load_library_permanently(str(SYSTEM_SHARED / name))

# Create some useful types
uchar_t = ir.IntType(16)
ustr_t = ir.PointerType(uchar_t)
int32_t = ir.IntType(32)
float32_t = ir.FloatType()
void_t = ir.VoidType()
bbmain_signature = ir.FunctionType(void_t, tuple())

int32_zero = ir.Constant(int32_t, 0)

class Backend:

    """Backend class: compile ast to llvm ir."""

    def __init__(self):
        """Init backend."""
        self.debug = False

        # Create an empty module...
        self.source_module = ir.Module()

        self.init_runtime()

        # and declare a function named "bbmain" inside it
        bbmain = ir.Function(self.source_module, bbmain_signature, name="bbmain")

        # Now implement the function
        block = bbmain.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        python_string = 'Привет, Мир!\00'
        ir_type = ir.ArrayType(uchar_t, len(python_string))
        ir_const = ir.Constant.literal_array([ir.Constant(uchar_t, ord(symbol)) for symbol in python_string])
        ir_global = ir.GlobalVariable(self.source_module, ir_type, 'hello')
        ir_global.global_constant = True
        ir_global.linkage = 'internal'
        ir_global.initializer = ir_const
        ir_global.align = 2

        llvm_address = self.builder.gep(ir_global, (int32_zero, int32_zero), inbounds=True)
        self.builder.call(self.runtime['Print'], (llvm_address, ))

        self.builder.ret_void()

    def init_runtime(self):
        """Init runtime libraries."""
        self.runtime = {
            'Print': ir.Function(self.source_module, ir.FunctionType(void_t, (ustr_t, )), 'Print')
        }

    def optimize(self, opt_level=2) -> binding.ModuleRef:
        """Compile and optimize llvm module."""
        llvm_module = binding.parse_assembly(str(self.source_module))
        llvm_module.verify()

        # Optimize
        pm = binding.create_module_pass_manager()
        pmb = binding.create_pass_manager_builder()
        pmb.opt_level = opt_level
        pmb.populate(pm)
        pm.run(llvm_module)

        return llvm_module

    @staticmethod
    def get_target_machine():
        """Return current target machine."""
        return binding.Target.from_default_triple().create_target_machine()

    def emit_assembly(self) -> str:
        """Optimize and return target assembler."""
        llvm_module = self.optimize()
        target_machine = self.get_target_machine()

        return target_machine.emit_assembly(llvm_module)

    def emit_llvm(self) -> str:
        """Optimize and return llvm ir."""
        llvm_module = self.optimize()
        return str(llvm_module)

    def run(self) -> None:
        """Run program."""
        binding.check_jit_execution()

        load_shared_library('libbbruntime_shared.so')
        load_shared_library('libicuuc.so')
        load_shared_library('libicuio.so')

        llvm_module = self.optimize()
        target_machine = self.get_target_machine()
        engine = binding.create_mcjit_compiler(llvm_module, target_machine)
        engine.finalize_object()
        engine.run_static_constructors()

        # main_ptr = engine.get_function_address('bbstart')
        bbinit_ptr = binding.address_of_symbol('bbinit')
        bbinit = ctypes.CFUNCTYPE(None)(bbinit_ptr)
        bbinit()

        bbmain_ptr = engine.get_function_address('bbmain')
        bbmain = ctypes.CFUNCTYPE(None)(bbmain_ptr)
        bbmain()

    def emit_executable(self, executable_filename: str):
        with tempfile.TemporaryDirectory() as source_dir:
            source_dir = pathlib.Path(source_dir)
            with open(str(source_dir / SOURCE_FILENAME), 'w') as output:
                output.write(self.emit_assembly())
            for filename in glob.iglob(str(SOURCE_DIRECTORY / '*')):
                shutil.copy2(filename, str(source_dir))

            build_dir = source_dir / 'build'
            build_dir.mkdir(parents=True, exist_ok=True)


            # cmake args
            config = 'Debug' if self.debug else 'Release'
            cmake_args = (
                '-DCMAKE_BUILD_TYPE=' + config,
            )

            # build args
            build_args = (
                '--config', config
            )

            subprocess.run(('cmake', '..') + cmake_args, stdout=sys.stdout.fileno(), stderr=sys.stderr.fileno(), cwd=build_dir, check=True)
            subprocess.run(('cmake', '--build', '.') + build_args, stdout=sys.stdout.fileno(), stderr=sys.stderr.fileno(), cwd=build_dir, check=True)

            shutil.copy2(str(build_dir / EXECUTABLE_FILENAME), executable_filename)
