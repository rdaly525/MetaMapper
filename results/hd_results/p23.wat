(module
  (type (;0;) (func))
  (type (;1;) (func (param i32) (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32) (result i32)
    local.get 0
    local.get 0
    i32.const 1
    i32.shr_u
    i32.const 357913941
    i32.and
    i32.sub
    i32.const 1
    i32.shl
    i32.const 1717986918
    i32.and
    local.tee 0
    i32.const 4
    i32.shr_u
    local.get 0
    i32.add
    i32.const 235802126
    i32.and)
  (memory (;0;) 256 256)
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "p23" (func 1))
  (export "_initialize" (func 0))
  )
