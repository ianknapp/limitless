import pytest
from pytest_factoryboy import register

from .cura_settings import (
    CuraSettingAdhesionType,
    CuraSettingSupportStruture,
    CuraSettingSupportType,
)
from .factories import ProjectFactory

register(ProjectFactory)


@pytest.fixture
def sample_project(sample_user, project_factory):
    project = project_factory(user=sample_user)
    return project


@pytest.mark.django_db
def test_project_cura_setting_defaults(sample_project):
    # Check defaults - of course we trust Django's ORM to set the defaults
    # properly. This is to safeguard against thoughtless or accidentaly changes
    # to these important settings.
    assert sample_project.enable_support is False
    assert sample_project.support_structure == CuraSettingSupportStruture.NORMAL
    assert sample_project.support_type == CuraSettingSupportType.EVERYWHERE
    assert sample_project.infill_sparse_density == 50
    assert sample_project.adhesion_type == CuraSettingAdhesionType.NONE


@pytest.mark.django_db
def test_project_cura_settings_str(sample_project):
    assert sample_project.cura_settings_str == ("-s infill_line_distance=2.4000000000000004 -s support_enable=false")

    sample_project.enable_support = True
    assert sample_project.cura_settings_str == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true -s support_structure=normal -s support_type=everywhere"
    )

    sample_project.support_structure = CuraSettingSupportStruture.TREE
    assert sample_project.cura_settings_str == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true -s support_structure=tree -s support_type=everywhere"
    )

    sample_project.adhesion_type = CuraSettingAdhesionType.BRIM
    assert sample_project.cura_settings_str == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true "
        "-s support_structure=tree -s support_type=everywhere -s adhesion_type=brim"
    )
