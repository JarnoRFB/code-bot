
class Template:

    def __init__(self, template_str, indices):
        self.template_str = template_str
        self.indices = indices

    def parse(self, message):
        self.parsed = tuple((word for i, word in enumerate(message.split()) if i in self.indices))

    def render(self):
        return self.template_str % (self.parsed)

def make_templates(beginner_template_str, advanced_template_str, indices):
    return (Template(beginner_template_str, indices),
            Template(advanced_template_str, advanced_template_str))