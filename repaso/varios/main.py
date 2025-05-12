from managers import FileReader, TextFileManager, BinaryFileManager


def show_custom_context_manager(file_path):
    with FileReader(file_path) as reader:
        reader.show_content()
    with FileReader(file_path) as reader:
        content = reader.get_content()
    
    print(f"content: {content}")


def read_text_file(file_path):
    manager = TextFileManager(file_path)
    content = manager.get_content()
    print(content)


def read_binary_file(file_path):
    manager = BinaryFileManager(file_path)
    content = manager.get_content()
    print(content)


def main():
    file_path = "sample.txt"
    # show_custom_context_manager(file_path)
    read_text_file(file_path)
    read_binary_file(file_path)


if __name__ == "__main__":
    main()
