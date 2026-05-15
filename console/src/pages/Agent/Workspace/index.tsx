import { useAgentsData, FileListPanel, FileEditor } from "./components";
import styles from "./index.module.less";

export default function WorkspacePage() {
  const {
    files,
    selectedFile,
    dailyMemories,
    expandedMemory,
    fileContent,
    loading,
    workspacePath,
    hasChanges,
    enabledFiles,
    setFileContent,
    fetchFiles,
    handleFileClick,
    handleDailyMemoryClick,
    handleSave,
    handleReset,
    handleToggleFileEnabled,
    handleReorderFiles,
  } = useAgentsData();

  return (
    <div className={styles.workspacePage}>
      <div className={styles.content}>
        <FileListPanel
          files={files}
          selectedFile={selectedFile}
          dailyMemories={dailyMemories}
          expandedMemory={expandedMemory}
          workspacePath={workspacePath}
          enabledFiles={enabledFiles}
          onRefresh={fetchFiles}
          onFileClick={handleFileClick}
          onDailyMemoryClick={handleDailyMemoryClick}
          onToggleEnabled={handleToggleFileEnabled}
          onReorder={handleReorderFiles}
        />

        <FileEditor
          selectedFile={selectedFile}
          fileContent={fileContent}
          loading={loading}
          hasChanges={hasChanges}
          onContentChange={setFileContent}
          onSave={handleSave}
          onReset={handleReset}
        />
      </div>
    </div>
  );
}
