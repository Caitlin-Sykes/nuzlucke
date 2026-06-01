package org.csykes.nuzlucke.repository;

import org.csykes.nuzlucke.entity.MilestoneEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

/**
 * Repository for managing Milestone entities.
 */
public interface MilestoneRepository extends JpaRepository<MilestoneEntity, Integer> {


    /**
     * Finds milestones for a given game slug, optionally up to a specified order index.
     * @param gameSlug The slug of the game to filter milestones by.
     * @param upTo The maximum order index to include in the result, or null to include all milestones.
     * @return A list of MilestoneEntity objects ordered by their order index.
     */
    @Query("""
            select m
            from MilestoneEntity m, GamesEntity g
            where g.name = :gameSlug
              and m.gameSlug = g.milestoneSlug
              and (:upTo is null or m.orderIndex <= :upTo)
            order by m.orderIndex asc
            """)
    List<MilestoneEntity> findMilestones(
            @Param("gameSlug") String gameSlug,
            @Param("upTo") Integer upTo
    );
}
