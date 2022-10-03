#!/usr/bin/env python
# coding: utf-8
# python 3.9

class ObjectExplorer:
    
    def __init__(self, object, show_values = True, show_help = True, show_protected = False, delim_value = 40, delim_out = "="*80, delim_in = "-"*80):
        object_name = f'{object=}'.split('=')[0]
        object_type = type(object).__name__
        print(f'{delim_out}')
        print(f'object_name:    {object_name}')
        print(f'object_type:    {object_type}')
        print(f'object_value:   {str(object)[:640]}')
        if not show_protected:
            object_methods = [method_name for method_name in dir(object) if callable(getattr(object, method_name)) and '__' not in method_name]
        else:
            object_methods = [method_name for method_name in dir(object) if callable(getattr(object, method_name))]
        print(f'{delim_in}')
        print(f'object_methods: {", ".join(object_methods)}')
        for object_method in object_methods:
            print(f'{delim_out}\n{object_method}\n{delim_out}')
            expression = f'object.{object_method}()'
            description = expression
            if show_values:
                if len(str(object)) < delim_value:
                    object_value_inline = str(object)
                else:
                    object_value_inline = str(object)[:delim_value] + '...'
                description = f'object="{object_value_inline}".{object_method}()'                
            try:
                result = eval(expression)
            except:
                result = 'ERROR'
            finally:
                print(f'{description} --> {result}')
                if show_help:
                    print(f'{delim_in}')
                    print(eval(f'object.{object_method}.__doc__'))
                    ## help(eval(f'object.{object_method}'))


object = "This is a simple text string on English language at 64 symbols!"
objectExplorer = ObjectExplorer(object)
