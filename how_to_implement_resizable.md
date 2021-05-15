# Resizable window support

```py
# initialise screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZEABLE)

# on resize
if event.type == pygame.VIDEO_RESIZE:
    size = min(event.x, event.y)
    screen = pygame.display.set_mode((size, size), pygame.RESIZEABLE)

# if drawing **before** resizing, run this inside instead
if event.type == pygame.VIDEO_RESIZE:
    size = min(event.x, event.y)
    old_screen = screen
    screen = pygame.display.set_mode((size, size), pygame.RESIZEABLE)
    screen.blit(old_screen)
    del old_screen
```

Don't forget to change the size of the FixedGrid and Solver *or* to refactor to use screen.get_size() or the equivalent
function.
