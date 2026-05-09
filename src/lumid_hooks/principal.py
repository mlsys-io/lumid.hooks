"""Identity envelope shared across hooks."""

from pydantic import BaseModel, ConfigDict, Field


class PrincipalContext(BaseModel):
    """Identity envelope returned by `IdentityProvider.resolve` and passed to every
    downstream hook."""

    model_config = ConfigDict(frozen=True)

    principal_id: str = Field(
        description="Stable id within the plugin's namespace; the project stamps "
        "this on owned resources."
    )
    org_id: str = Field(description="Tenant the principal belongs to.")
    external_id: str = Field(
        description="External handle (email, OIDC `sub`, etc.). Plugin-defined."
    )
    principal_type: str = Field(
        description='Descriptive label (e.g. `"user"`, `"admin"`). Diagnostic only; '
        "capability decisions belong in `scopes`."
    )

    scopes: list[str] = Field(
        description="Capabilities the principal carries, in a plugin-defined "
        "vocabulary."
    )
