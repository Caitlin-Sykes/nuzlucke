package org.csykes.nuzlucke.dto;

/**
 * DTO for game illustration.
 * @param imageUrl
 * @param imageAuthor
 * @param imageRights
 * @param imageSource
 */
public record IllustrationDto(
        String imageUrl,
        String imageAuthor,
        String imageRights,
        String imageSource
) {
}
