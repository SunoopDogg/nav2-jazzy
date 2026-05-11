from setuptools import setup
from glob import glob
import os

package_name = 'nav2_custom_worlds'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'models', 'go2'),
         [f for f in glob('models/go2/*') if os.path.isfile(f)]),
        (os.path.join('share', package_name, 'models', 'go2', 'meshes'), glob('models/go2/meshes/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='aswoo55555@gmail.com',
    description='Nav2 simulation launch files for AWS RoboMaker worlds',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [],
    },
)
