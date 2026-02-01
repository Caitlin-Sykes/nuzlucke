package org.csykes.nuzlucke.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.csykes.nuzlucke.entity.GamesEntity;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class GamesDto {
    
    private String name;
    private String creator;
    private String platform;
    private Integer[] generationsIncluded;
    private Boolean isRomHack;
    private ReleaseDates releaseDate;
    private Credits credits;

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ReleaseDates {
        private LocalDate releaseDateEu;
        private LocalDate releaseDateJp;
        private LocalDate releaseDateAu;
        private LocalDate releaseDateUs;
    }

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Credits {
        private String imageCredits;
        private String imageRights;
        private String imageUrl;
    }

    public static GamesDto fromEntity(GamesEntity game) {
        /**
         * Converts a GamesEntity to a GamesDto.
         * @param game GamesEntity to convert.
         */
        return new GamesDto(
                game.getName(),
                game.getCreator(),
                game.getPlatform(),
                game.getGenerationsIncluded(),
                game.getIsRomHack(),
                new GamesDto.ReleaseDates(
                        game.getReleaseDateEu(),
                        game.getReleaseDateJp(),
                        game.getReleaseDateAu(),
                        game.getReleaseDateUs()
                ),
                new GamesDto.Credits(
                        game.getImageCredits(),
                        game.getImageRights(),
                        game.getImageUrl()
                )
        );
    }
}

