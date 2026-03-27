package org.csykes.nuzlucke.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.csykes.nuzlucke.entity.GamesEntity;

import java.time.LocalDate;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class GamesDto {
    private Integer id;
    private String name;
    private String creator;
    private String platform;
    private Integer[] generationsIncluded;
    private Integer rulesetId;
    private Integer regionId;
    private Boolean isRomHack;
    private Boolean isDlc;
    private ReleaseDates releaseDate;
    private Credits credits;
    private String regionName;
    private String description;
    private String isRomHackOf;
    private Boolean hasFakemon;
    private String difficultyLevel;
    private String[] qolFeatures;

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
            GamesDto dto = new GamesDto();

            dto.setId(game.getId());
            dto.setName(game.getName());
            dto.setPlatform(game.getPlatform());
            dto.setGenerationsIncluded(game.getGenerationsIncluded());
            dto.setRulesetId(game.getRulesetId());
            dto.setRegionId(game.getRegionId());
            dto.setIsRomHack(game.getIsRomHack());
            dto.setIsDlc(game.getIsDlc());
            dto.setDescription(game.getDescription());
            dto.setRegionName(game.getRegion() != null ? game.getRegion().getName() : null);
    
            return dto;
        }
}

