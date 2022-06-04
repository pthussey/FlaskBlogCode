from flask import Flask, render_template, url_for, request
from flask_flatpages import FlatPages
import emoji

app = Flask(__name__)

# Configure settings for FLATPAGES
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['fenced_code', 'codehilite']

# Initialize flatpages
flatpages = FlatPages(app)


# Adds a template filter to render emoji shortcodes
@app.template_filter('emojify')
def emoji_filter(s):
    return emoji.emojize(s, use_aliases=True)


# Home route
@app.route("/")
def home():
    posts_by_date = sorted(list(flatpages), reverse=True,
                    key=lambda page: page.meta['published'])
    return render_template('home.html', posts=posts_by_date)


# About route
@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Configure URL routing for each blog post by the name of Markdown file
@app.route("/post/<name>")
def post(name):
    post = flatpages.get_or_404(name)
    return render_template('blog_post.html', post=post, title=post.meta['title'])


if __name__ == '__main__':
    app.run(debug=True)