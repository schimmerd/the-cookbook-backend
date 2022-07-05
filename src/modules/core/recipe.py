import os

from src.modules.helper import allowed_file, detect_text
from src.modules.gcp.storage import upload
from src.modules.gcp.datastore import create_new_recipe, get_recipes


def add_new_recipe(kw, isTM, files):
    try:
        if 'files[]' not in files:
            return 'Error: No file part', None
        files = files.getlist('files[]')

        for file in files:
            filename = file.filename
            if file and allowed_file(filename):
                # UPLOAD FILE TO GCS
                error, dest_name = upload(file=file, name=filename)
                if error:
                    return error
                # DETECT TEXT
                url = 'gs://{}/{}'.format(os.environ.get('BUCKET_NAME'), dest_name)
                error, texts = detect_text(uri=url)
                if error:
                    return error
                raw_text = texts[0].description
                # SAVE PARAMS ON DATA STORE
                link = 'https://{}/{}'.format(os.environ.get('LINK_PREFIX'), dest_name)
                # error = save_recipe(text=raw_text, uri=url, link=link, kw=kw, isTM=isTM)
                error = create_new_recipe(text=raw_text, uri=url, link=link, kw=kw, isTM=isTM)
                if error:
                    return error
        return None
    except Exception as exc:
        return 'Service unable to check file upload: {}'.format(exc)


def get_all_recipes():
    try:
        error, recipe_list = get_recipes()
        if error:
            return error, None
        return None, recipe_list
    except Exception as exc:
        return 'Service unable to get all recipes: {}'.format(exc), None
