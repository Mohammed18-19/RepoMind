export interface SidebarListProps {
  repositoryId?: number
}

export function SidebarList({ repositoryId }: SidebarListProps) {
  return (
    <div className="flex-1 overflow-auto">
      <div className="p-8 text-center">
        <p className="text-sm text-muted-foreground">
          No conversations yet
        </p>
      </div>
    </div>
  )
}
