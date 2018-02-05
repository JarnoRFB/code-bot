
class Template:

    def __init__(self, template_str, indices):
        self.template_str = template_str
        self.indices = indices

    def parse(self, message):
        return tuple((word for i, word in enumerate(message.split()) if i in self.indices))

    def render(self, context):
        parsed = tuple((word for i, word in enumerate(context['message'].split()) if i in self.indices))
        formated_template = 'In line %d you ' % context['line']
        formated_template += self.template_str % (parsed)
        formated_template += ' Do you want to correct or ignore the error?'
        return formated_template


def make_templates(beginner_template_str, advanced_template_str, indices):
    return (Template(beginner_template_str, indices),
            Template(advanced_template_str, indices))