package org.csykes.nuzlucke.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

import java.util.Map;

/**
 * Entity representing game metadata in the database.
 * 1:1 relationship with {@link GamesEntity}.
 */
@Getter
@Setter
@Entity
@Table(name = "game_metadata")
public class GameMetaDataEntity {
    @Id
    @Column(name = "game_id", nullable = false)
    private Integer id;

    @MapsId
    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "game_id", nullable = false)
    private GamesEntity games;

    @ColumnDefault("false")
    @Column(name = "has_fakemon")
    private Boolean hasFakemon;

    @ColumnDefault("true")
    @Column(name = "stats_modified")
    private Boolean statsModified;

    @ColumnDefault("false")
    @Column(name = "is_complete")
    private Boolean isComplete;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "rom_hack_of_game_id")
    private GamesEntity romHackOfGame;

    @Column(name = "engine_type", columnDefinition = "game_engine")
    private Object engineType;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "qol_features")
    private Map<String, Object> qolFeatures;

    @Column(name = "difficulty_level", length = 50)
    private String difficultyLevel;

    @ColumnDefault("true")
    @Column(name = "unique_story")
    private Boolean uniqueStory;


}