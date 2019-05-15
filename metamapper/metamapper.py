import coreir

class MetaMapper:
    def __init__(self,context : coreir.context,namespace_name):
        self.backend_modules = set()
        self.rules = []

        self.context = context
        self.ns = context.new_namespace(namespace_name)

    def add_rewrite_rule(self,rule):
        self.rules.append(rule)

    def add_backend_primitive(self, prim : coreir.module.Module):
        self.backend_modules.add(prim)

    def add_const(self,width):
        c = self.context
        if width==1:
            cnst = c.get_namespace("corebit").modules["const"]
        else:
            cnst = c.get_namespace("coreir").generators["const"](width=width)
        self.add_backend_primitive(cnst)

    def map_app(self,app : coreir.module.Module):
        self.context.run_passes(['flatten','flattentypes'])
        changed = False
        for rule in self.rules:
            changed |= rule(app)

        # Verify that all the instances in the application have the same type as the primitive list.
        adef = app.definition
        for inst in adef.instances:
            if inst.module not in self.backend_modules:
                app.print_()
                raise Exception(f"{inst.name}:{inst.module.name} is not a backend_primitive\n prims: {str([mod.name for mod in self.backend_modules])}")

