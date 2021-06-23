import glob
import os
import shutil

from django.conf import settings
from tqdm import tqdm


class BibBuilder:
    from_dir = settings.FMBIBS_DIR
    to_dir = os.path.join(settings.BASE_DIR, 'article', 'templates', 'article', 'fmbibs')

    def build(self):
        # clean files in to_dir
        if os.path.exists(self.to_dir):
            shutil.rmtree(self.to_dir)
        os.mkdir(self.to_dir)
        # list files from from_dir
        paths = glob.glob(os.path.join(self.from_dir, "*.bib"))
        # write files to to_dir
        for from_path in tqdm(paths, desc='Creating fmbibs'):
            basename = os.path.basename(from_path)
            to_path = os.path.join(self.to_dir, basename)
            shutil.copy(from_path, to_path)
