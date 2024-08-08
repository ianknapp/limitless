from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Settings(TextChoices):
    ADHESION_TYPE = "adhesion_type", _("Adhesion Type")
    SUPPORT_ENABLE = "support_enable", _("Enable Supports")
    SUPPORT_STRUCTURE = "support_structure", _("Support Structure")
    SUPPORT_TYPE = "support_type", _("Support Type")
    INFILL_SPARSE_DENSITY = "infill_sparse_density", _("Infill Percentage")
    INFILL_LINE_DISTANCE = "infill_line_distance", _("Infill Line Distance")


class SupportStruture(TextChoices):
    NORMAL = "normal", _("Normal")
    TREE = "tree", _("Tree")


class SupportType(TextChoices):
    BUILDPLATE = "buildplate", _("Buildplate")
    EVERYWHERE = "everywhere", _("Everywhere")


class AdhesionType(TextChoices):
    SKIRT = "skirt", _("Skirt")
    BRIM = "brim", _("Brim")
    RAFT = "raft", _("Raft")
    NONE = "none", _("None")


def cura_settings_str(settings):
    settings = {
        Settings.INFILL_LINE_DISTANCE: compute_infill_line_distance(settings.infill_sparse_density),
        Settings.SUPPORT_ENABLE: ("true" if settings.enable_support else "false"),
        **(
            {
                Settings.SUPPORT_STRUCTURE: settings.support_structure,
                Settings.SUPPORT_TYPE: settings.support_type,
            }
            if settings.enable_support
            else {}
        ),
        **({Settings.ADHESION_TYPE: settings.adhesion_type} if settings.adhesion_type != AdhesionType.NONE else {}),
    }
    return " ".join(f"-s {key}={value}" for key, value in settings.items())


def compute_infill_line_distance(infill_sparse_density=50, infill_line_width=0.4, infill_pattern="cubic"):
    """Logic taken from the Cura frontend. The defaults are from the CuraEngine source on GitHub:

    https://github.com/Ultimaker/Cura/tree/main/resources/definitions/fdmprinter.def.json

    This shows how the more options we enable for users, the more edge cases we will have to
    implement in our settings.
    """
    return (
        0
        if infill_sparse_density == 0
        else (infill_line_width * 100)
        / infill_sparse_density
        * (
            2
            if infill_pattern == "grid"
            else (
                3
                if infill_pattern == "triangles"
                or infill_pattern == "trihexagon"
                or infill_pattern == "cubic"
                or infill_pattern == "cubicsubdiv"
                else (
                    2
                    if infill_pattern == "tetrahedral" or infill_pattern == "quarter_cubic"
                    else (1 if infill_pattern == "cross" or infill_pattern == "cross_3d" else (1.6 if infill_pattern == "lightning" else 1))
                )
            )
        )
    )
