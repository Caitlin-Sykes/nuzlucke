package org.csykes.nuzlucke.mapper;

import org.csykes.nuzlucke.dto.GamesDto;
import org.csykes.nuzlucke.dto.CreditsDto;
import org.csykes.nuzlucke.dto.IllustrationDto;
import org.csykes.nuzlucke.entity.GameMetaDataEntity;
import org.csykes.nuzlucke.dto.ReleaseDatesDto;
import org.csykes.nuzlucke.entity.GamesEntity;

import java.time.LocalDate;
import java.util.Map;

/**
 * Maps {@link GamesEntity} to {@link GamesDto}.
 */
public final class GamesMapper {

    private GamesMapper() {
    }

    public static GamesDto toDto(GamesEntity game) {
        return new GamesDto(
                game.getId(),
                game.getName(),
                game.getPlatform(),
                game.getGenerationsIncluded(),
                game.getRulesetId(),
                game.getRegionId(),
                game.getIsRomHack(),
                game.getIsDlc(),
                toReleaseDates(game.getReleaseDates()),
                toCredits(game.getGameCredits()),
                toIllustration(game.getIllustration()),
                game.getRegion() != null ? game.getRegion().getName() : null,
                game.getDescription(),
                getMetadata(game) != null && getMetadata(game).getRomHackOfGame() != null
                        ? getMetadata(game).getRomHackOfGame().getName()
                        : null,
                getMetadata(game) != null ? getMetadata(game).getHasFakemon() : null,
                getMetadata(game) != null ? getMetadata(game).getDifficultyLevel() : null,
                getMetadata(game) != null ? toQolFeatures(getMetadata(game).getQolFeatures()) : null
        );
    }

    private static GameMetaDataEntity getMetadata(GamesEntity game) {
        return game.getMetadata();
    }

    private static ReleaseDatesDto toReleaseDates(Map<String, Object> releaseDates) {
        if (releaseDates == null || releaseDates.isEmpty()) {
            return null;
        }

        Map<String, Object> values = releaseDates;
        Object nested = releaseDates.get("releaseDate");
        if (nested instanceof Map<?, ?> nestedMap) {
            @SuppressWarnings("unchecked")
            Map<String, Object> nestedValues = (Map<String, Object>) nestedMap;
            values = nestedValues;
        }

        return new ReleaseDatesDto(
                readDate(values, "eu"),
                readDate(values, "jp"),
                readDate(values, "au"),
                readDate(values, "us")
        );
    }

    private static CreditsDto toCredits(Map<String, Object> credits) {
        if (credits == null || credits.isEmpty()) {
            return null;
        }

        Map<String, Object> values = credits;
        Object nested = credits.get("credits");
        if (nested instanceof Map<?, ?> nestedMap) {
            @SuppressWarnings("unchecked")
            Map<String, Object> nestedValues = (Map<String, Object>) nestedMap;
            values = nestedValues;
        }

        return new CreditsDto(
                asString(readValue(values, "game_rights")),
                asString(readValue(values, "game_creator"))
        );
    }

    private static IllustrationDto toIllustration(Map<String, Object> illustration) {
        if (illustration == null || illustration.isEmpty()) {
            return null;
        }

        Map<String, Object> values = illustration;
        Object nested = illustration.get("illustration");
        if (nested instanceof Map<?, ?> nestedMap) {
            @SuppressWarnings("unchecked")
            Map<String, Object> nestedValues = (Map<String, Object>) nestedMap;
            values = nestedValues;
        }

        return new IllustrationDto(
                asString(readValue(values, "image_url", "imageUrl", "url")),
                asString(readValue(values, "image_author", "imageAuthor", "author")),
                asString(readValue(values, "image_rights", "imageRights", "rights")),
                asString(readValue(values, "image_source", "imageSource", "source"))
        );
    }

    private static Object readValue(Map<String, Object> values, String... keys) {
        for (String key : keys) {
            if (values.containsKey(key)) {
                return values.get(key);
            }
        }
        return null;
    }

    private static String asString(Object value) {
        return value == null ? null : value.toString();
    }

    private static String[] toQolFeatures(Map<String, Object> qolFeatures) {
        if (qolFeatures == null || qolFeatures.isEmpty()) {
            return null;
        }

        return qolFeatures.values().stream()
                .map(Object::toString)
                .toArray(String[]::new);
    }

    private static LocalDate readDate(Map<String, Object> values, String... keys) {
        for (String key : keys) {
            if (values.containsKey(key)) {
                return asLocalDate(values.get(key));
            }
        }
        return null;
    }

    private static LocalDate asLocalDate(Object value) {
        if (value == null) {
            return null;
        }
        if (value instanceof LocalDate localDate) {
            return localDate;
        }
        return LocalDate.parse(value.toString());
    }
}
