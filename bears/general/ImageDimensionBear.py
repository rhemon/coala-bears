import os
import yaml
import shutil

from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.GemRequirement import GemRequirement
from dependency_management.requirements.PipRequirement import PipRequirement
from sarge import run, Capture


class ImageDimensionBear(GlobalBear):
    """
    Checks the dimension of an image.

    More information is available at <github.com/Abhi2424shek/img_checker>
    """

    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    REQUIREMENTS = {GemRequirement(' img_checker'),
                    PipRequirement('pyyaml', '3.12')}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Image Dimension'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('img_checker') is None:
            return 'img_checker is not installed.'
        return True

    def run(self,
            image_file,
            width,
            height):

        with open('img_config.yml', 'w') as yaml_file:
            config = [{'directory': image_file,
                       'width': width,
                       'height': height}]
            yaml.dump(config, yaml_file, default_flow_style=False)
        cmd = 'img_checker'
        output = run(cmd, stdout=Capture(), stderr=Capture())
        if (output.returncode):
            lines = output.stdout.text.split('\n')[1:-2]
            for line in lines:
                if '.png' in line:
                    fileName = line[10:line.index('.png')+4]
                if '.jpg' in line:
                    fileName = line[10:line.index('.jpg')+4]
                yield Result.from_values(origin=self,
                                         message=line,
                                         file=fileName,
                                         severity=RESULT_SEVERITY.NORMAL)

        os.remove('img_config.yml')
