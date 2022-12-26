from flask import Flask, render_template, redirect
import sqlite3

app =  Flask(__name__)

@app.route('/', methods="POST")
def content_add_db():
    pass

