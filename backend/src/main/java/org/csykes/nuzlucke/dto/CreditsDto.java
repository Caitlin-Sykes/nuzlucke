package org.csykes.nuzlucke.dto;

/**
 * DTO for game credits.
 * @param gameRights - rights to the game
 * @param gameCreator - creator of the game
 */
public record CreditsDto(
        String gameRights,
        String gameCreator
) {
}
