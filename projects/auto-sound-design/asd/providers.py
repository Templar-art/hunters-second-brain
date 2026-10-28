"""Optional sound-generation providers, for categories the local library can't cover.

Nothing here is wired to a real service yet, on purpose:
- Paid generation is OFF by default (config "generation.enabled": false).
- No provider is implemented until its current API docs, pricing and licence terms have
  been checked. There is no Soundbot integration; one has not been verified to exist.
- Keys come from environment variables only (e.g. ASD_<PROVIDER>_API_KEY), never source.
- Before any upload, paid request or licensed download, the tool must ask and get a typed yes.

To add one later: subclass SoundProvider, register it in PROVIDERS, and keep `requires_approval`.
"""

import os
from abc import ABC, abstractmethod


class ProviderDisabled(RuntimeError):
    pass


class SoundProvider(ABC):
    name = "base"
    env_key = None  # e.g. "ASD_ELEVENLABS_API_KEY"
    paid = True
    uploads_media = False

    def api_key(self):
        if not self.env_key:
            return None
        key = os.environ.get(self.env_key)
        if not key:
            raise ProviderDisabled(f"{self.name}: set {self.env_key} in your environment (never in a file in this repo)")
        return key

    @abstractmethod
    def estimate_cost(self, category, seconds):
        """Return a human-readable cost quote without spending anything."""

    @abstractmethod
    def generate(self, category, seconds, out_path, prompt):
        """Create one sound file at out_path. Only called after explicit approval."""


class NullProvider(SoundProvider):
    """Default: generates nothing and says what is missing."""
    name = "none"
    paid = False

    def estimate_cost(self, category, seconds):
        return "free (nothing is generated)"

    def generate(self, category, seconds, out_path, prompt):
        raise ProviderDisabled("No generation provider is configured; add your own sounds for this category.")


PROVIDERS = {"none": NullProvider}


def get_provider(cfg):
    gen = cfg.get("generation", {})
    if not gen.get("enabled"):
        return NullProvider()
    name = gen.get("provider", "none")
    if name not in PROVIDERS:
        raise ProviderDisabled(f"Provider '{name}' is not implemented. Verified providers: {', '.join(PROVIDERS)}")
    return PROVIDERS[name]()


def request_approval(provider, category, seconds, ask=input):
    """Every paid or uploading call goes through here. Returns True only on a typed 'yes'."""
    if not provider.paid and not provider.uploads_media:
        return True
    quote = provider.estimate_cost(category, seconds)
    answer = ask(f"{provider.name} would generate a {seconds:.1f}s {category} ({quote}). Type 'yes' to approve: ")
    return answer.strip().lower() == "yes"
