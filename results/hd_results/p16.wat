(module
  (type (;0;) (func))
  (type (;1;) (func (param i32 i32) (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32 i32) (result i32)
    local.get 1
    local.get 0
    local.get 0
    local.get 1
    i32.lt_u
    select)
  (memory (;0;) 256 256)
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "p16" (func 1))
  (export "_initialize" (func 0))
  )
