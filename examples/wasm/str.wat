(module
 (table 0 anyfunc)
 (memory $0 1)
 (data (i32.const 16) "Hello World!\00")
 (export "memory" (memory $0))
 (export "get" (func $get))
 (func $get (; 0 ;) (result i32)
  (i32.const 16)
 )
)
