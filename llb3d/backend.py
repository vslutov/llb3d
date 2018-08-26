# from ctypes import CFUNCTYPE, c_int8
#
# import llvmlite.binding as llvm
# from llvmlite import ir
#
# # Create some useful types
# int8_t = ir.IntType(8)
# fnty = ir.FunctionType(int8_t, tuple())
#
# # Create an empty module...
# module = ir.Module()
# # and declare a function named "bb_main" inside it
# func = ir.Function(module, fnty, name="bb_main")
#
# # Now implement the function
# block = func.append_basic_block(name="entry")
# builder = ir.IRBuilder(block)
#
# a = builder.alloca(int8_t, name="a")
# ten = ir.Constant(int8_t, 10)
# builder.store(ten, a)
# result = builder.load(a)
# builder.ret(result)
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
# func_ptr = engine.get_function_address("bb_main")
#
# # Run the function via ctypes
# cfunc = CFUNCTYPE(c_int8)(func_ptr)
# res = cfunc()
# print("Result is", res)
