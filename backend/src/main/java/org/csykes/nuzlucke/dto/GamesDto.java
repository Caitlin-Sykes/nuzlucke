package org.csykes.nuzlucke.dto;

/**
 * DTO for game data.
 * @param id
 * @param name
 * @param platform
 * @param generationsIncluded
 * @param rulesetId
 * @param regionId
 * @param isRomHack
 * @param isDlc
 * @param releaseDate
 * @param credits
 * @param illustration
 * @param regionName
 * @param description
 * @param isRomHackOf
 * @param hasFakemon
 * @param difficultyLevel
 * @param qolFeatures
 */
public record GamesDto(
        Integer id,
        String name,
        String platform,
        Integer[] generationsIncluded,
        Integer rulesetId,
        Integer regionId,
        Boolean isRomHack,
        Boolean isDlc,
        ReleaseDatesDto releaseDate,
        CreditsDto credits,
        IllustrationDto illustration,
        String regionName,
        String description,
        String isRomHackOf,
        Boolean hasFakemon,
        String difficultyLevel,
        String[] qolFeatures
) {
}
