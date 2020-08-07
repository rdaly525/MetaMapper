(module
 (table 0 anyfunc)
 (memory $0 1)
 (export "memory" (memory $0))
 (export "add3" (func $add3))
 (func $add3 (; 0 ;) (param $0 i32) (param $1 i32) (param $2 i32) (result i32)
  (i32.add
   (get_local $2)
   (i32.add
    (get_local $1)
    (get_local $0)
   )
  )
 )
)
