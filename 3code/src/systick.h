// balmer@inbox.ru RLC Meter 303
// 2013-2014

#ifndef __SYSTICK_H
#define __SYSTICK_H 

#include <stdint.h>
#include "stm32f30x.h"

#define IS_SYSTICK_CLK_SOURCE(SOURCE) (((SOURCE) == SysTick_CLKSource_HCLK) || \
                                       ((SOURCE) == SysTick_CLKSource_HCLK_Div8))

/* SysTick counter state */
#define SysTick_Counter_Disable        ((u32)0xFFFFFFFE)
#define SysTick_Counter_Enable         ((u32)0x00000001)
#define SysTick_Counter_Clear          ((u32)0x00000000)

#define IS_SYSTICK_COUNTER(COUNTER) (((COUNTER) == SysTick_Counter_Disable) || \
                                     ((COUNTER) == SysTick_Counter_Enable)  || \
                                     ((COUNTER) == SysTick_Counter_Clear))

/* SysTick Flag */
#define SysTick_FLAG_COUNT             ((u32)0x00000010)
#define SysTick_FLAG_SKEW              ((u32)0x0000001E)
#define SysTick_FLAG_NOREF             ((u32)0x0000001F)

#define IS_SYSTICK_FLAG(FLAG) (((FLAG) == SysTick_FLAG_COUNT) || \
                               ((FLAG) == SysTick_FLAG_SKEW)  || \
                               ((FLAG) == SysTick_FLAG_NOREF))

#define IS_SYSTICK_RELOAD(RELOAD) (((RELOAD) > 0) && ((RELOAD) <= 0xFFFFFF))


/* ---------------------- SysTick registers bit mask -------------------- */
/* CTRL TICKINT Mask */
#define CTRL_TICKINT_Set      ((uint32_t)0x00000002)
#define CTRL_TICKINT_Reset    ((uint32_t)0xFFFFFFFD)

void SysTick_SetReload(uint32_t Reload);
void SysTick_CounterCmd(uint32_t SysTick_Counter);
void SysTick_ITConfig(FunctionalState NewState);
u32 SysTick_GetCounter(void);
FlagStatus SysTick_GetFlagStatus(uint8_t SysTick_FLAG);


void delay_init(void);
void delay_ms(uint16_t nms);
void delay_us(uint32_t nus);

#endif
