from typing import List

from models import Tag, Language, Link, Profile


# create link
# add tag (existing or not)
# set language(s)

def get_links_by_tags(tags: List[str]):
    return Link.objects.filter(tags__in=tags)


def get_links_by_tags_and_languages(tags: List[str], languages: List[str]):
    return Link.objects.filter(tags__in=tags, languages__in=languages)


def add_tag_to_link(link_id: int, tag_name: str):
    link = Link.objects.get(id=link_id)
    tag = Tag.objects.get_or_create(name=tag_name)
    link.tags.add(tag[0])


def remove_tag_from_link(link_id: int, tag_name: str):
    link = Link.objects.get(id=link_id)
    link.tags.remove()
