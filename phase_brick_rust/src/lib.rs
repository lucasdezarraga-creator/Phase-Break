use pyo3::prelude::*;
use rand::prelude::*;

// A simple structure to represent our bricks without PyGame Rect objects!
#[derive(Clone)]
struct Brick {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
    color_index: usize,
}

// Expose our PhaseBricksRust class directly to Python!
#[pyclass]
struct PhaseBricksRust {
    paddle_x: f32,
    ball_x: f32,
    ball_y: f32,
    ball_velo_x: f32,
    ball_velo_y: f32,
    current_ball_color_idx: usize,
    bricks: Vec<Brick>,
}

#[pymethods]
impl PhaseBricksRust {
    #[new]
    fn new() -> Self {
        let mut env = PhaseBricksRust {
            paddle_x: 515.0, // (1280 / 2) - (250 / 2)
            ball_x: 640.0,
            ball_y: 585.0, // 610 - 25 (Paddle top - radius)
            ball_velo_x: 315.0, // 450 * 0.7
            ball_velo_y: -315.0, // -450 * 0.7
            current_ball_color_idx: 3,
            bricks: Vec::new(),
        };
        env.reset_game();
        env
    }

    // Mirrors your env.reset() function
    fn reset(&mut self) -> (f32, f32, f32, f32, f32, usize) {
        self.reset_game();
        (
            self.paddle_x,
            self.ball_x,
            self.ball_y,
            self.ball_velo_x,
            self.ball_velo_y,
            self.current_ball_color_idx,
        )
    }

    // Mirrors your env.step() function
    fn step(&mut self, action: i32, dt: f32) -> ((f32, f32, f32, f32, f32, usize), f32, bool) {
        let mut reward = 0.0;
        let mut done = false;

        // 1. Handle Paddle Movement Actions
        if action == 0 {
            self.paddle_x -= 450.0 * dt;
        } else if action == 2 {
            self.paddle_x += 450.0 * dt;
        }

        // Clamp paddle to window walls
        if self.paddle_x < 0.0 {
            self.paddle_x = 0.0;
        } else if self.paddle_x + 250.0 > 1280.0 {
            self.paddle_x = 1280.0 - 250.0;
        }

        // 2. Advance Ball Position
        self.ball_x += self.ball_velo_x * dt;
        self.ball_y += self.ball_velo_y * dt;

        // Reward standing near the ball
        let paddle_center = self.paddle_x + 125.0;
        let ball_dist = (paddle_center - self.ball_x).abs();
        reward += (0.0f32).max(0.5 * (1.0 - (ball_dist / 1280.0)));

        // 3. Wall Collisions
        if self.ball_x - 25.0 < 0.0 {
            self.ball_x = 25.0;
            self.ball_velo_x *= -1.0;
        } else if self.ball_x + 25.0 > 1280.0 {
            self.ball_x = 1280.0 - 25.0;
            self.ball_velo_x *= -1.0;
        }

        if self.ball_y - 25.0 < 0.0 {
            self.ball_y = 25.0;
            self.ball_velo_y *= -1.0;
        }

        // Drop Ball (Death Condition)
        if self.ball_y - 25.0 > 720.0 {
            reward = -1000.0;
            done = true;
        }

        // 4. Paddle Collision Logic
        if self.ball_y + 25.0 >= 610.0 && self.ball_y - 25.0 <= 640.0
            && self.ball_x + 25.0 >= self.paddle_x && self.ball_x - 25.0 <= self.paddle_x + 250.0 
        {
            self.ball_y = 610.0 - 25.0;
            self.ball_velo_y *= -1.0;
            reward = 200.0;

            if self.ball_x < paddle_center {
                self.ball_velo_x -= 100.0;
            } else {
                self.ball_velo_x += 100.0;
            }
            self.ball_velo_x = (-400.0f32).max((400.0f32).min(self.ball_velo_x));

            // Choose a random color index from our 4 available choices using modern rand API
            let mut rng = rand::rng();
            let choices = [0, 1, 2, 3];
            self.current_ball_color_idx = *choices.choose(&mut rng).unwrap();
        }

        // 5. Brick Collisions Logic
        let mut hit_index: Option<usize> = None;
        for (i, brick) in self.bricks.iter().enumerate() {
            // Check overlapping collision between Ball and Brick
            if self.ball_x + 25.0 >= brick.x && self.ball_x - 25.0 <= brick.x + brick.width
                && self.ball_y + 25.0 >= brick.y && self.ball_y - 25.0 <= brick.y + brick.height 
            {
                hit_index = Some(i);
                break;
            }
        }

        if let Some(idx) = hit_index {
            let brick = &self.bricks[idx];
            
            // basic bounce swap for velocity
            if self.ball_x < brick.x || self.ball_x > brick.x + brick.width {
                self.ball_velo_x *= -1.0;
            } else {
                self.ball_velo_y *= -1.0;
            }

            if self.current_ball_color_idx == brick.color_index {
                self.bricks.remove(idx);
                reward = 100.0;
                if self.bricks.is_empty() {
                    reward = 1000.0;
                    done = true;
                }
            } else {
                reward = -5.0;
            }
        }

        let state_tuple = (
            self.paddle_x,
            self.ball_x,
            self.ball_y,
            self.ball_velo_x,
            self.ball_velo_y,
            self.current_ball_color_idx,
        );

        (state_tuple, reward, done)
    }
}

// Helper block to generate the initial board setup
impl PhaseBricksRust {
    fn reset_game(&mut self) {
        self.paddle_x = 515.0;
        self.ball_x = 640.0;
        self.ball_y = 585.0;
        self.ball_velo_x = 315.0;
        self.ball_velo_y = -315.0;
        self.current_ball_color_idx = 3;
        self.bricks.clear();
    }
}