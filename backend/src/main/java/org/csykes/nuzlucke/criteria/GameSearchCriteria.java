package org.csykes.nuzlucke.criteria;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Criteria used for filtering games based on various parameters.
 * @param filter - The search filter for game names, case-insensitive
 * @param gen - The generation of the game to filter by
 * @param region - The region of the game to filter by
 * @param platform - The platform of the game to filter by
 */
public record GameSearchCriteria(
        
        @Schema(description = "Fuzzy search for game names (e.g., 'Red' or 'Leaf')", example = "Emerald")
        String nameLike,

        @Schema(description = "The generation the game was released in", example = "3")
        Integer gen,

        @Schema(description = "The region name where the game takes place", example = "Hoenn")
        String region,
        
        @Schema(description = "The console or handheld platform a game was released for", example = "Game Boy Advance")
        String platform,
        
        @Schema(description = "Filter by whether the game is DLC or a base game", defaultValue = "false")
        Boolean isDlc
) {}
