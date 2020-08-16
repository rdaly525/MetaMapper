(module
  (type (;0;) (func))
  (type (;1;) (func (param i32 i32 i32 i32) (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32 i32 i32 i32) (result i32)
    local.get 2
    local.get 3
    local.get 0
    local.get 1
    i32.eq
    select
    local.get 1
    local.get 3
    i32.xor
    i32.const 0
    local.get 0
    local.get 3
    i32.eq
    select
    i32.xor)
  (memory (;0;) 256 256)
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "p21" (func 1))
  (export "_initialize" (func 0))
  )
