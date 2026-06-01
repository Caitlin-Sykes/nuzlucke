package org.csykes.nuzlucke.controllers;

import lombok.extern.log4j.Log4j2;
import org.csykes.nuzlucke.entity.MilestoneEntity;
import org.csykes.nuzlucke.repository.MilestoneRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@Log4j2
@RequestMapping("/milestones")
public class MilestoneController {

    private final MilestoneRepository milestoneRepository;

    public MilestoneController(MilestoneRepository milestoneRepository) {
        this.milestoneRepository = milestoneRepository;
    }

    /**
     * Returns list of milestones for a specific game
     * Can return up to a specific number
     * @param game
     * @param number
     * @return
     */
    @GetMapping("/{game}")
    public List<MilestoneEntity> getMilestone(@PathVariable String game, @RequestParam(required=false) Integer number) {
        log.debug(">> getMilestone");
        List<MilestoneEntity> milestones = milestoneRepository.findMilestones(game, number);
        log.debug("<< getMilestone");
        return milestones;
    }
}
