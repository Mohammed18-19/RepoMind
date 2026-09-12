'use client'

import Link from 'next/link'
import { cn } from '@/lib/utils'
import { buttonVariants } from '@/components/ui/button'
import { IconMessage } from '@/components/ui/icons'

interface SidebarItemProps {
  id: string | number
  title: string
  href: string
  active?: boolean
}

export function SidebarItem({
  id,
  title,
  href,
  active
}: SidebarItemProps) {
  return (
    <div className="relative" key={id}>
      <div className="absolute left-2 top-1 flex h-6 w-6 items-center justify-center">
        <IconMessage className="h-4 w-4" />
      </div>

      <Link
        href={href}
        className={cn(
          buttonVariants({ variant: 'ghost' }),
          'group w-full pl-8 pr-4',
          active && 'bg-accent'
        )}
      >
        <div className="flex w-full items-center overflow-hidden">
          <span className="whitespace-nowrap truncate">{title}</span>
        </div>
      </Link>
    </div>
  )
}
