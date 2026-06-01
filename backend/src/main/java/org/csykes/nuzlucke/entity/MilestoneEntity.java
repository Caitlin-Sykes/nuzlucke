package org.csykes.nuzlucke.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;

@Getter
@Setter
@Entity
@Table(name = "milestones")
public class MilestoneEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Integer id;

    @Size(max = 100)
    @NotNull
    @Column(name = "stage_name", nullable = false, length = 100)
    private String stageName;

    @NotNull
    @Column(name = "level_cap", nullable = false)
    private Integer levelCap;

    @NotNull
    @Column(name = "order_index", nullable = false)
    private Integer orderIndex;

    @Size(max = 50)
    @Column(name = "game_slug", length = 50)
    private String gameSlug;

    @ColumnDefault("false")
    @Column(name = "unlocks_surf")
    private Boolean unlocksSurf;

    @ColumnDefault("false")
    @Column(name = "has_fishing_rod")
    private Boolean hasFishingRod;


}