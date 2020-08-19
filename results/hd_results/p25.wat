(module
  (type (;0;) (func))
  (type (;1;) (func (param i32 i32) (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    local.get 1
    i32.const 65535
    i32.and
    local.tee 2
    local.get 0
    i32.const 65535
    i32.and
    local.tee 3
    i32.mul
    i32.const 16
    i32.shr_u
    local.get 2
    local.get 0
    i32.const 16
    i32.shr_s
    local.tee 0
    i32.mul
    i32.add
    local.tee 2
    i32.const 16
    i32.shr_s
    local.get 0
    local.get 1
    i32.const 16
    i32.shr_s
    local.tee 0
    i32.mul
    i32.add
    local.get 0
    local.get 3
    i32.mul
    local.get 2
    i32.const 65535
    i32.and
    i32.add
    i32.const 16
    i32.shr_s
    i32.add)
  (memory (;0;) 256 256)
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "p25" (func 1))
  (export "_initialize" (func 0))
  )
