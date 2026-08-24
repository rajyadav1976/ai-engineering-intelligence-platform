from __future__ import annotations

from engineering_intelligence_llm.domain.protocols import LLMProvider


class ProviderRegistry:
    """Registry of available LLM providers."""

    def __init__(self) -> None:
        self._providers: dict[str, LLMProvider] = {}

    def register(self, provider: LLMProvider) -> None:
        """Register an LLM provider by its name."""

        if provider.name in self._providers:
            raise ValueError(
                f"LLM provider '{provider.name}' is already registered"
            )

        self._providers[provider.name] = provider

    def get(self, name: str) -> LLMProvider:
        """Return a registered provider by name."""

        try:
            return self._providers[name]
        except KeyError as exc:
            raise ValueError(
                f"LLM provider '{name}' is not registered"
            ) from exc

    def contains(self, name: str) -> bool:
        """Return True when a provider is registered."""

        return name in self._providers

    def names(self) -> tuple[str, ...]:
        """Return the names of all registered providers."""

        return tuple(self._providers.keys())