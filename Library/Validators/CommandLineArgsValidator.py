from typing import Any

class CommandLineArgsValidator:

    @staticmethod
    def validate(args: Any):
        target_keys = [
            'user_inputs',
            'appsettings'
        ]
        for key in target_keys:
            try:
                filepath = getattr(args, key)
            except Exception as ex:
                raise ValueError(f'Expected args to have setting {key}')

if __name__ == '__main__':
    pass