##简介
实现注册功能，然后基于 flask-login 插件实现用户登录功能。
用户在输入表单数据时，不可能每次都是符合我们后台要求的，所以，另一个任务是在后台使用 wtform 对表单数据进行验证，失败时，在前台页面友好的提示错误信息。
另外，表单的渲染和错误信息的提示，这些都是通用的，我们会将这些东西封装为 jinja2 的一个宏（macro）。

####知识点
1. Flask Web 框架
2. Flask-login 登录功能
3. WTForm 数据验证
4. Jinja2 模板

####使用宏macro渲染表单
jinja2 的 macro 和 Python 的函数一样，可以对重复的动作进行封装。函数可以传入不同的参数，macro 也是可以的。
macro 的基本语法：
```
{% macro macro_name(arg1, arg2, ...) %}
  ...
{% endmacro %}
```
macro 通常集中存放在 macros.html 文件中,导入语法：
```
{% from "macros.html" import macro_name %}
```
调用一个 macro 时，要将它放入 {{ }} 中：
```
{{ macro_name(arg1, arg2, ...) }}
```
下面实现了一个 render_form 的宏用于渲染表单
```
<!-- 需要传入2个参数：要渲染的 form 和点击提交请求的 url -->
{% macro render_form(form, url) %}
<form method="POST" action="{{ url }}">
  <!-- 将 csrf_token 渲染在表单开始的位置 -->
  {{ form.csrf_token }}
  <!-- 迭代每个表单 field -->
  {% for field in form %}
    <!-- 如果是 csrf_token 就不再渲染了 -->
    {% if field.type == 'CSRFTokenField' %}
    {{ '' }}
    <!-- SubmitField 单独特殊处理 -->
    {% elif field.type == 'SubmitField' %}
    {{ form.submit(class='btn btn-primary', type='submit') }}
    <!-- BooleanField 单独特殊处理 -->
    {% elif field.type == 'BooleanField' %}
    <div class="checkbox">
      <label>{{ field() }} {{ field.label.text }}</label>
    </div>
    {% else %}
    <div class="form-group">
      {{ field.label }} {{ field(class='form-control') }}
    </div>
    {% endif %}
  {% endfor %}
</form>
{% endmacro %}
```