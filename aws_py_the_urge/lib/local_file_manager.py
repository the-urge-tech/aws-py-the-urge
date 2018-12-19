import gzip
import logging
import os.path
import re
from zipfile import ZipFile

LOG = logging.getLogger(__name__)


class LocalFileManager(object):
    def __init__(self, file):
        self.file = file

    def get_feed_content(self):
        feed_content = None
        local_uncompressed_output = re.sub(r'\.(gz|zip)$', '', self.file)

        def save_uncompressed(feed_content, local_uncompressed_output):
            with open(local_uncompressed_output, 'wb') as f2:
                LOG.debug("Saving uncompressed copy at: {}".format(
                    local_uncompressed_output))
                f2.write(feed_content)

        if os.path.exists(local_uncompressed_output):
            LOG.debug("Using already uncompressed file: {}".format(
                local_uncompressed_output))
            with open(local_uncompressed_output, 'rb') as f:
                return f.read()

        if self.file.endswith('.gz'):
            with gzip.open(self.file, 'rb') as f:
                LOG.debug("Uncompressing file: {}".format(self.file))
                feed_content = f.read()
                save_uncompressed(feed_content, local_uncompressed_output)

        if self.file.endswith('.zip'):
            with open(self.file, 'rb') as f:
                z = ZipFile(f)
                zfile = z.namelist()[0]
                feed_content = z.read(zfile)
                save_uncompressed(feed_content, local_uncompressed_output)

        return feed_content
