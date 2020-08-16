(module
  (type (;0;) (func))
  (type (;1;) (func (param i32) (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32) (result i32)
    (local i32)
    i32.const 0
    local.get 0
    i32.sub
    local.get 0
    i32.and
    local.tee 1
    local.get 0
    i32.xor
    i32.const 2
    i32.shr_s
    local.get 1
    i32.div_s
    local.get 0
    local.get 1
    i32.add
    i32.or)
  (memory (;0;) 256 256)
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "p20" (func 1))
  (export "_initialize" (func 0))
  )
