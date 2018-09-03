import tempfile
import pathlib
import shutil
import glob
import subprocess
import sys

from llvmlite import ir, binding

SOURCE_DIRECTORY = pathlib.Path(__file__).parent.resolve() / 'bbprogram'
SOURCE_FILENAME = 'bbprogram.s'
EXECUTABLE_FILENAME = 'bbprogram'

# All these initializations are required for code generation!
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()  # yes, even this one

class Backend:

    """Backend class: compile ast to llvm ir."""

    # Create some useful types
    int8_t = ir.IntType(8)
    cstr_t = ir.PointerType(int8_t)
    int32_t = ir.IntType(32)
    float32_t = ir.FloatType()
    void_t = ir.VoidType()
    bbmain_signature = ir.FunctionType(void_t, tuple())

    def __init__(self):
        """Init backend."""
        self.debug = False

        # Create an empty module...
        self.source_module = ir.Module()

        self.init_runtime()

        # and declare a function named "bbmain" inside it
        bbmain = ir.Function(self.source_module, self.bbmain_signature, name="bbmain")

        # Now implement the function
        block = bbmain.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        self.builder.ret_void()

    def init_runtime(self):
        """Init runtime libraries."""
        self.runtime = {
            'Print': ir.Function(self.source_module, ir.FunctionType(self.void_t, (self.cstr_t, )), 'Print')
        }

    def emit_assembly(self) -> str:
        """Optimize and compile module."""
        llvm_module = binding.parse_assembly(str(self.source_module))
        llvm_module.verify()

        # Optimize
        pm = binding.create_module_pass_manager()
        pmb = binding.create_pass_manager_builder()
        pmb.opt_level = 2
        pmb.populate(pm)
        pm.run(llvm_module)

        target_machine = binding.Target.from_default_triple().create_target_machine()

        return target_machine.emit_assembly(llvm_module)

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
