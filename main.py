import errno
import os
import re


class PythonUrl:

  def __init__(self, filepath):
    # checking if file exist else raising a file not found error
    if not os.path.exists(filepath):
      raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                              filepath)

    self.file = filepath
    self.tag_expresion = re.compile(
      r"(?:href|src)=(\"|\')((?!mailto|https).*?static.*?)(\"|\')")
    self.path_expression = re.compile(r"static(/|\\)(.*)")

  def to_flask(self, django=False):

    with open(self.file, "r") as f:
      file_content = f.read()
      file_content_list = file_content.split("\n")
      # setting the regular expression to find any link and src tag

      #loopping through the each line in the file
      for line in file_content_list:
        match = self.tag_expresion.finditer(line)
        for item in match:
          print(item.group(2))
          link = self.path_expression.search(item.group(2)).group(2)

          if django:
            file_content = file_content.replace(item.group(2),
                                                "{% static '" + link + "' %}")
          else:
            file_content = file_content.replace(
              item.group(2), "{{url_for('static', filename='" + link + "}')}}")
          # file_content.replace(item.group(2), item.)

      #replacing thec

      with open("new.html", 'w') as ff:
        # print(file_content)
        ff.write(file_content)

  def to_django(self):
    pass


file = PythonUrl("index.html")
file.to_url(django=True)
