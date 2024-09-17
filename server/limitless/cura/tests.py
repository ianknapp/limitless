import pytest
from pytest_factoryboy import register

from .factories import ProjectFactory
from .settings import AdhesionType, SupportStructure, SupportType, cura_settings_str

register(ProjectFactory)


@pytest.fixture
def sample_project(sample_user, project_factory):
    project = project_factory(user=sample_user)
    return project


@pytest.mark.django_db
def test_project_cura_setting_defaults(sample_project):
    # Check defaults - of course we trust Django's ORM to set the defaults
    # properly. This is to safeguard against thoughtless or accidental changes
    # to these important settings.
    settings = sample_project.settings
    assert settings.enable_support is False
    assert settings.support_structure == SupportStructure.NORMAL
    assert settings.support_type == SupportType.EVERYWHERE
    assert settings.infill_sparse_density == 50
    assert settings.adhesion_type == AdhesionType.NONE


@pytest.mark.django_db
def test_project_cura_settings_str(sample_project):
    settings = sample_project.settings
    assert cura_settings_str(settings) == ("-s infill_line_distance=2.4000000000000004 -s support_enable=false")

    settings.enable_support = True
    assert cura_settings_str(settings) == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true -s support_structure=normal -s support_type=everywhere"
    )

    settings.support_structure = SupportStructure.TREE
    assert cura_settings_str(settings) == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true -s support_structure=tree -s support_type=everywhere"
    )

    settings.adhesion_type = AdhesionType.BRIM
    assert cura_settings_str(settings) == (
        "-s infill_line_distance=2.4000000000000004 -s support_enable=true "
        "-s support_structure=tree -s support_type=everywhere -s adhesion_type=brim"
    )

    settings.infill_sparse_density = 20
    assert cura_settings_str(settings) == (
        "-s infill_line_distance=6.0 -s support_enable=true -s support_structure=tree -s support_type=everywhere -s adhesion_type=brim"
    )
