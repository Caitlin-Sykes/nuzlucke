package org.csykes.nuzlucke.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDate;

@Entity
@Table(name = "games")
@Getter
@Setter
@NoArgsConstructor
public class GamesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(name = "ruleset_id", nullable = false)
    private Integer rulesetId;

    @Column(name = "region_id")
    private Integer regionId;

    @Column(name = "api_version_id")
    private Integer apiVersionId;

    @Column(name = "is_rom_hack")
    private Boolean isRomHack;

    @Column(name = "image_url")
    private String imageUrl;

    @Column(name = "image_rights", length = 255)
    private String imageRights;

    @Column(name = "image_credits", length = 255)
    private String imageCredits;

    @Column(name = "release_date_us")
    private LocalDate releaseDateUs;

    @Column(name = "release_date_jp")
    private LocalDate releaseDateJp;

    @Column(name = "release_date_eu")
    private LocalDate releaseDateEu;

    @Column(name = "release_date_au")
    private LocalDate releaseDateAu;

    @Column(name = "platform", length = 50)
    private String platform;

    @Column(name = "creator", length = 50)
    private String creator;

    @JdbcTypeCode(SqlTypes.ARRAY)
    @Column(name = "generations_included", columnDefinition = "integer[]")
    private Integer[] generationsIncluded;

    @Column(name = "is_dlc")
    private Boolean isDlc;
}