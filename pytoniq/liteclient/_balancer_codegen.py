codegen_text1 = '''    """CODE BELOW IS AUTOGENERATED. DO NOT EDIT MANUALLY"""\n\n'''
codegen_text2 = '''    """CODE ABOVE IS AUTOGENERATED. DO NOT EDIT MANUALLY"""\n\n'''


def main():

    with open('client.py', 'r') as f:
        offset = False
        lines = f.readlines()

        result = codegen_text1
        tmp = ''

        for line in lines:
            if 'async def get_masterchain_info(self):' in line:
                offset = True
            if not offset:
                continue
            if 'async def' in line:
                tmp += line
                name = line[line.index('    async def ') + 14: line.index('(')]
            if tmp and ':\n' in line:
                if name not in line:
                    tmp += line
                tmp = tmp.replace('):', ', **kwargs):')
                tmp = tmp.replace(') ->', ', **kwargs) ->')
                tmp += '    ' * 2 + f"return await self.execute_method('{name}', **self._get_args(locals())) \n\n"
                result += tmp
                tmp = ''
            elif tmp:
                if name not in line:
                    tmp += line

        result += codegen_text2

    with open('balancer.py', 'r') as f:
        text = f.read()
        new_text = text[:text.index(codegen_text1)] + result + text[text.index(codegen_text2) + len(codegen_text2):]

    with open('balancer.py', 'w') as f:
        f.write(new_text)


if __name__ == '__main__':
    main()
