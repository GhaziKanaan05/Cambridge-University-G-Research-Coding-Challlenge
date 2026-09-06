def assign_tasks(factor, arrival, bonus, reward, duration, time_bonus):
    T = len(arrival)  # Number of tasks
    P = len(factor[0])  # Number of processors
    schedule = [None] * T  # To store (processor, start_time) for each task
    processor_availability = [0] * P  # Tracks when each processor is next available

    # List of tasks to be scheduled, with indices
    tasks = list(range(T))

    while tasks:
        best_task = None
        best_processor = None
        best_start_time = None
        best_score = -float('inf')

        # Dynamically evaluate each task based on current state of processor availability
        for i in tasks:
            task_best_score = -float('inf')
            task_best_processor = None
            task_best_start_time = None

            for p in range(P):
                # Determine the earliest possible start time for the task on this processor
                start_time = max(arrival[i], processor_availability[p])
                within_bonus_time = start_time < arrival[i] + time_bonus[i]

                # Calculate potential score
                if within_bonus_time:
                    score = factor[i][p] * (bonus[i] + reward[i] * duration[i] / (duration[i] + start_time - arrival[i]))
                else:
                    score = factor[i][p] * (reward[i] * duration[i] / (duration[i] + start_time - arrival[i]))

                # Apply reward decay factor: prioritize tasks close to losing bonus by a higher multiplier
                time_until_bonus_expires = arrival[i] + time_bonus[i] - start_time
                if time_until_bonus_expires > 0:
                    decay_factor = 1 + (1 / (1 + time_until_bonus_expires))
                else:
                    decay_factor = 0.9  # Apply a penalty if already missed the bonus window
                
                score *= decay_factor

                # Apply task duration normalization to slightly prioritize shorter tasks
                score /= (1 + duration[i] / 50.0)

                # Update best option if this processor offers a better score for the task
                if score > task_best_score:
                    task_best_score = score
                    task_best_processor = p
                    task_best_start_time = start_time

            # Update the overall best task assignment
            if task_best_score > best_score:
                best_score = task_best_score
                best_task = i
                best_processor = task_best_processor
                best_start_time = task_best_start_time

        # Assign the selected best task to its best processor and start time
        schedule[best_task] = (best_processor, best_start_time)
        processor_availability[best_processor] = best_start_time + duration[best_task]

        # Remove the scheduled task from remaining tasks
        tasks.remove(best_task)

	return schedule