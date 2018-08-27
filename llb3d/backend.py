# from ctypes import CFUNCTYPE
#
# import llvmlite.binding as llvm
# from llvmlite import ir
#
# # Create some useful types
# int8_t = ir.IntType(8)
# void_t = ir.VoidType()
# fnty = ir.FunctionType(void_t, tuple())
# hello_world = ir.Constant.literal_array('Hello, World!')
#
# # Create an empty module...
# module = ir.Module()
# # and declare a function named "bbmain" inside it
# bbmain = ir.Function(module, fnty, name="bbmain")
#
# # Now implement the function
# block = bbmain.append_basic_block(name="entry")
# builder = ir.IRBuilder(block)
#
# builder.call('Print', (hello_world, ))
#
# # All these initializations are required for code generation!
# llvm.initialize()
# llvm.initialize_native_target()
# llvm.initialize_native_asmprinter()  # yes, even this one
#
#
# def create_execution_engine():
#     """
#     Create an ExecutionEngine suitable for JIT code generation on
#     the host CPU.  The engine is reusable for an arbitrary number of
#     modules.
#     """
#     # Create a target machine representing the host
#     target = llvm.Target.from_default_triple()
#     target_machine = target.create_target_machine()
#     # And an execution engine with an empty backing module
#     backing_mod = llvm.parse_assembly("")
#     engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
#     return engine
#
#
# def optimize(module) -> None:
#     """
#     Optimize llvm code.
#     """
#     pm = llvm.create_module_pass_manager()
#     pmb = llvm.create_pass_manager_builder()
#     pmb.opt_level = 3
#     pmb.populate(pm)
#     pm.run(module)
#
#
# def compile_ir(engine: llvm.ExecutionEngine, llvm_ir: str):
#     """
#     Compile the LLVM IR string with the given engine.
#     The compiled module object is returned.
#     """
#     # Create a LLVM module object from the IR
#     module = llvm.parse_assembly(llvm_ir)
#     module.verify()
#     # Now add the module and make sure it is ready for execution
#     engine.add_module(module)
#     optimize(module)
#     engine.finalize_object()
#     engine.run_static_constructors()
#     return module
#
#
# engine = create_execution_engine()
#
# # Print the module IR
# llvm_ir = str(module)
# module = compile_ir(engine, llvm_ir)
# print(str(module))
#
# # Look up the function pointer (a Python int)
# func_ptr = engine.get_function_address("bbmain")
#
# # Run the function via ctypes
# cfunc = CFUNCTYPE(None)(func_ptr)
# cfunc()
