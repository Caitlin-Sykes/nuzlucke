package org.csykes.nuzlucke.entity;

import jakarta.persistence.*;
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
}