import metamapper.wasm.interp as interp

def test_add():
    vm = interp.load('./examples/wasm/add.wasm')
    r = vm.exec('add', [4, 5])
    assert r == 9

def test_fib():
    vm = interp.load('./examples/wasm/fib.wasm')
    r = vm.exec('fib', [10])
    assert r == 55

def test_env():
    def _fib(n):
        if n <= 1:
            return n
        return _fib(n - 1) + _fib(n - 2)


    def fib(_: interp.Ctx, n: int):
        return _fib(n)

    vm = interp.load('./examples/wasm/env.wasm', {'env': {'fib': fib}})
    r = vm.exec('get', [10])
    assert r == 55

def test_str():
    vm = interp.load('./examples/wasm/str.wasm')
    r = vm.exec('get', [])
    assert vm.store.mems[0].data[r:r + 12] == b'Hello World!'

def test_sum():
    vm = interp.load('./examples/wasm/sum.wasm')
    r = vm.exec('sum', [100])
    assert r == 4950
