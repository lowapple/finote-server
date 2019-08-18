from mongoengine import *
import tasks

connect(
    'cupfin'
)

tasks.sync()