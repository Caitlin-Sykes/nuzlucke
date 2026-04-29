package org.csykes.nuzlucke.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.csykes.nuzlucke.converter.JsonMapConverter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.Map;

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

    @Column(name = "is_rom_hack")
    private Boolean isRomHack;

    @Column(name = "platform", length = 50)
    private String platform;

    @JdbcTypeCode(SqlTypes.ARRAY)
    @Column(name = "generations_included", columnDefinition = "integer[]")
    private Integer[] generationsIncluded;

    @Column(name = "is_dlc")
    private Boolean isDlc;
    
    @Column(name="description")
    private String description;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "region_id", insertable = false, updatable = false)
    private RegionEntity region;
     
    @Column(name = "illustration", columnDefinition = "jsonb")
    @Convert(converter = JsonMapConverter.class)
    private Map<String, Object> illustration;
    
    @Column(name = "game_credits", columnDefinition = "jsonb")
    @Convert(converter = JsonMapConverter.class)
    private Map<String, Object> gameCredits;
    
    @Column(name = "release_dates", columnDefinition = "jsonb")
    @Convert(converter = JsonMapConverter.class)
    private Map<String, Object> releaseDates;
    
    @ColumnDefault("false")
    @Column(name = "has_alternate_forms")
    private Boolean hasAlternateForms;
    
    @ColumnDefault("false")
    @Column(name = "has_mega_evolution")
    private Boolean hasMegaEvolution;

    @OneToOne(mappedBy = "games", fetch = FetchType.LAZY, optional = true)
    private GameMetaDataEntity metadata;
}
